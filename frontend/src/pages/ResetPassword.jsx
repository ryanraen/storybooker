import { useState } from "react";
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Stack,
} from "@mui/material";
import { useNavigate, useSearchParams } from "react-router";

export default function ResetPassword() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const access_token = searchParams.get("access_token"); // token in url as ?token=...
  const refresh_token = searchParams.get("refresh_token");

  const [new_password, setNewPassword] = useState("");
  const [error, setError] = useState("");

  const handleReset = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await fetch("http://localhost:5000/user/reset-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ new_password, access_token, refresh_token }),
      });

      if (!res.ok) throw new Error("Password reset failed");

      navigate("/login");
    } catch (err) {
      setError("Unable to reset password.");
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
          Reset Password
        </Typography>
        <Typography color="text.secondary" mb={3}>
          Enter your new password below.
        </Typography>

        <form onSubmit={handleReset}>
          <Stack spacing={3}>
            <TextField
              label="New Password"
              type="password"
              fullWidth
              value={new_password}
              onChange={(e) => setNewPassword(e.target.value)}
              required
            />

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
              Reset Password
            </Button>
          </Stack>
        </form>
      </Paper>
    </Box>
  );
}
