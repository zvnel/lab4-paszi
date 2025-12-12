import React, { useState } from "react";
import "./App.css";

type ApiError = {
  detail?: any;
};

// Нормализуем сообщения об ошибках валидации
const prettifyError = (msg: string): string => {
  if (!msg) return "";

  // убираем "Value error, "
  let m = msg.replace(/^Value error,\s*/i, "");

  // стандартные ошибки Pydantic на английском
  m = m.replace(
    "String should have at least 3 characters",
    "Логин должен содержать минимум 3 символа"
  );
  m = m.replace(
    "String should have at least 8 characters",
    "Пароль должен быть не короче 8 символов"
  );

  return m;
};

const App: React.FC = () => {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setSuccessMessage(null);
    setErrorMessage(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ login, password }),
      });

      if (response.status === 201) {
        const data = await response.json();

        // API по ТЗ возвращает "user создан", а на фронте показываем по-русски
        const raw = data.message as string;
        const pretty =
          raw === "user создан" ? "Пользователь успешно создан" : raw;

        setSuccessMessage(pretty);
        setLogin("");
        setPassword("");
      } else if (response.status === 409) {
        const data: ApiError = await response.json();
        const detail = data.detail;

        const msg =
          typeof detail === "string"
            ? detail
            : "Пользователь с таким логином уже существует";

        setErrorMessage(msg);
      } else if (response.status === 422) {
        const data: ApiError = await response.json();
        let msg = "Ошибка валидации данных";

        if (Array.isArray(data.detail) && data.detail.length > 0) {
          const mapped = data.detail
            .map((err: any) => prettifyError(err.msg || ""))
            .filter((s: string) => s && s.trim().length > 0);

          // убираем дубли
          const unique = Array.from(new Set(mapped));

          if (unique.length > 0) {
            msg = unique.join("; ");
          }
        }

        setErrorMessage(msg);
      } else {
        setErrorMessage("Неизвестная ошибка сервера");
      }
    } catch (err) {
      console.error(err);
      setErrorMessage("Не удалось подключиться к серверу");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="card">
        <h1>Регистрация</h1>

        <form onSubmit={handleSubmit} className="form">
          <label>
            Логин
            <input
              type="text"
              value={login}
              onChange={(e) => setLogin(e.target.value)}
              placeholder="Введите логин"
              required
            />
          </label>

          <label>
            Пароль
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Введите пароль"
              required
            />
          </label>

          <button type="submit" disabled={loading}>
            {loading ? "Отправка..." : "Зарегистрироваться"}
          </button>
        </form>

        {successMessage && (
          <div className="message success">{successMessage}</div>
        )}
        {errorMessage && <div className="message error">{errorMessage}</div>}

        <div className="hint">
          <p>
            Требования к паролю: минимум 8 символов, хотя бы одна строчная, одна
            заглавная буква, цифра и спецсимвол.
          </p>
        </div>
      </div>
    </div>
  );
};

export default App;
