const API_URL =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";


export async function resolveCustomer(message) {
  const response = await fetch(
    `${API_URL}/api/resolve`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      },

      body: JSON.stringify({
        message
      })
    }
  );


  if (!response.ok) {
    let detail = "Unable to resolve customer request.";

    try {
      const errorData = await response.json();

      if (errorData.detail) {
        detail = errorData.detail;
      }
    } catch {
      // Ignore JSON parsing failure.
    }

    throw new Error(detail);
  }


  return response.json();
}


export async function checkBackend() {
  const response = await fetch(
    `${API_URL}/`
  );

  if (!response.ok) {
    throw new Error(
      "Backend is not available."
    );
  }

  return response.json();
}