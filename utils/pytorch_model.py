import torch
import torch.nn as nn
import torch.optim as optim
import os

MODEL_PATH = "cost_predictor_model.pth"
class CostPredictor(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )

    def forward(self, x):
        return self.model(x)


class CostPredictionService:
    def __init__(self):
        self.model = None
        self.trained = False
        self.load_model_if_exists()

    def load_model_if_exists(self):
        if os.path.exists(MODEL_PATH):
            self.model = CostPredictor(input_size=1)  # створення моделі
            self.model.load_state_dict(torch.load(MODEL_PATH))
            self.model.eval()
            self.trained = True
        else:
            self.model = CostPredictor(input_size=1)
    def preprocess_data(self, stages):
        cleaned = []
        for stage in stages:
            if stage["actual"] < stage["planned"] * 0.7:
                cleaned.append({**stage, "actual": 0})
            else:
                cleaned.append(stage)
        return cleaned

    def is_data_sufficient(self, stages):
        non_zero_actuals = [s for s in stages if s["actual"] > 0]
        return len(stages) > 3 and len(non_zero_actuals) / len(stages) >= 0.5

    def train_and_predict(self, stages):
        stages = self.preprocess_data(stages)

        known = [s for s in stages if s["actual"] > 0]
        unknown = [s for s in stages if s["actual"] == 0]

        if not self.is_data_sufficient(known):
            return None

        X = [[s["planned"]] for s in known]
        y = [[s["actual"]] for s in known]

        X_tensor = torch.tensor(X, dtype=torch.float32)
        y_tensor = torch.tensor(y, dtype=torch.float32)

        # Якщо модель уже була натренована – продовжуємо донавчання
        optimizer = optim.Adam(self.model.parameters(), lr=0.005)
        loss_fn = nn.MSELoss()

        for _ in range(500):  # менше епох, якщо донавчання
            preds = self.model(X_tensor)
            loss = loss_fn(preds, y_tensor)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        self.trained = True

        # Зберігаємо модель
        torch.save(self.model.state_dict(), MODEL_PATH)

        # Прогнозування
        with torch.no_grad():
            predicted_actuals = []
            for s in unknown:
                pred = self.model(torch.tensor([[s["planned"]]], dtype=torch.float32)).item()
                predicted_actuals.append(pred)

        total = sum(s["actual"] for s in known) + sum(predicted_actuals)
        return round(total)

