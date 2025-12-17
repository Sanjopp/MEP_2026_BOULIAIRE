export const API_BASE = "/api";

function getAuthHeaders() {
  const token = localStorage.getItem("access_token");
  return token
    ? { Authorization: `Bearer ${token}` }
    : {};
}

async function handleResponse(res) {
  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new Error(data.error || `HTTP ${res.status}`);
  }

  return data;
}

export async function login(email, password) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await handleResponse(res);

  localStorage.setItem("access_token", data.access_token);

  return data;
}

export function logout() {
  localStorage.removeItem("access_token");
}

export async function register({ name, email, password }) {
  const res = await fetch("/api/auth/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name,
      email,
      password,
    }),
  });

  return handleResponse(res);
}

export async function fetchTricounts() {
  const res = await fetch(`${API_BASE}/tricounts`, {
    headers: {
      ...getAuthHeaders(),
    },
  });
  return handleResponse(res);
}

export async function fetchTricountDetail(id) {
  const res = await fetch(`${API_BASE}/tricounts/${id}`, {
    headers: {
      ...getAuthHeaders(),
    },
  });
  return handleResponse(res);
}

export async function createTricount(name) {
  const res = await fetch(`${API_BASE}/tricounts`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify({ name }),
  });
  return handleResponse(res);
}

export async function deleteTricount(id) {
  const res = await fetch(`${API_BASE}/tricounts/${id}`, {
    method: "DELETE",
    headers: {
      ...getAuthHeaders(),
    },
  });
  return handleResponse(res);
}

export async function addUser(tricountId, payload) {
  const res = await fetch(`${API_BASE}/tricounts/${tricountId}/users`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function deleteUser(tricountId, userId) {
  const res = await fetch(
    `${API_BASE}/tricounts/${tricountId}/users/${userId}`,
    {
      method: "DELETE",
      headers: {
        ...getAuthHeaders(),
      },
    }
  );
  return handleResponse(res);
}

export async function addExpense(tricountId, payload) {
  const res = await fetch(`${API_BASE}/tricounts/${tricountId}/expenses`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function deleteExpense(tricountId, expenseId) {
  const res = await fetch(
    `${API_BASE}/tricounts/${tricountId}/expenses/${expenseId}`,
    {
      method: "DELETE",
      headers: {
        ...getAuthHeaders(),
      },
    }
  );
  return handleResponse(res);
}

export async function exportExcel(tricountId) {
  const res = await fetch(
    `${API_BASE}/tricounts/${tricountId}/export/excel`,
    {
      headers: {
        ...getAuthHeaders(),
      },
    }
  );

  if (!res.ok) {
    throw new Error("Export failed");
  }

  return res.blob();
}
