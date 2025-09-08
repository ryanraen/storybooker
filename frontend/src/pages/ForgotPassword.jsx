import { useState } from "react";
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Stack,
} from "@mui/material";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const reset_page = window.location.origin + "/reset-password";

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");

    try {
      const res = await fetch("http://localhost:5000/user/forgot-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, reset_page }),
      });

      if (!res.ok) throw new Error("Failed to send reset email");

      setMessage("Check your email for a reset link.");
    } catch (err) {
      setError("Unable to send reset email.");
      console.log(err.message);
    }
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        bgcolor: "#f9fafb",
        p: 2,
      }}
    >
      <Paper sx={{ p: 5, borderRadius: 3, boxShadow: 3, maxWidth: 420, width: "100%" }}>
        <Typography variant="h5" fontWeight="bold" gutterBottom>
          Forgot Password
        </Typography>
        <Typography color="text.secondary" mb={3}>
          Enter your email and we’ll send you a reset link.
        </Typography>

        <form onSubmit={handleSubmit}>
          <Stack spacing={3}>
            <TextField
              label="Email"
              type="email"
              fullWidth
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            {message && <Typography color="success.main">{message}</Typography>}
            {error && <Typography color="error">{error}</Typography>}

            <Button
              type="submit"
              variant="contained"
              fullWidth
              sx={{
                bgcolor: "black",
                "&:hover": { bgcolor: "#111" },
                borderRadius: 2,
                textTransform: "none",
                py: 1.3,
              }}
            >
              Send Reset Link
            </Button>
          </Stack>
        </form>
      </Paper>
    </Box>
  );
}
