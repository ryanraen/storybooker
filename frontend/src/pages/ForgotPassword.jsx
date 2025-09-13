import { useState } from "react";
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Stack,
} from "@mui/material";
import { useNavigate } from "react-router";

export default function ForgotPassword() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [otp, setOtp] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [disabled, setDisabled] = useState(false);

  const handleSendOtp = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");
    setDisabled(true);

    try {
      const res = await fetch(
        `${import.meta.env.PROD ? import.meta.env.VITE_PROD_API_URL : import.meta.env.VITE_DEV_API_URL}/user/forgot-password`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email }),
        }
      );
      if (!res.ok) throw new Error("Failed to send OTP");

      setOtpSent(true);
      setMessage("Code sent! Check your email for the 6-digit code.");
    } catch {
      setError("Unable to send OTP. Try again.");
    }
    setDisabled(false);
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");

    try {
      const res = await fetch(`${import.meta.env.PROD ? import.meta.env.VITE_PROD_API_URL : import.meta.env.VITE_DEV_API_URL}/user/verify-otp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, otp, password }),
      });

      if (!res.ok) throw new Error("OTP verification failed");

      setMessage("Password reset successful! You can now log in.");
      setOtpSent(false);
      setOtp("");
      setPassword("");
      navigate("/login", {
        state: {
          successMessage: "Password reset successful! You can now log in.",
        },
      });
    } catch {
      setError("Invalid OTP or unable to reset password.");
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
      <Paper
        sx={{
          p: 5,
          borderRadius: 3,
          boxShadow: 3,
          maxWidth: 420,
          width: "100%",
        }}
      >
        <Typography variant="h5" fontWeight="bold" gutterBottom>
          Reset Password
        </Typography>
        <Typography color="text.secondary" mb={3}>
          Enter your email to receive a 6-digit code.
        </Typography>

        <form onSubmit={otpSent ? handleResetPassword : handleSendOtp}>
          <Stack spacing={3}>
            <TextField
              label="Email"
              type="email"
              fullWidth
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            {/* shown after OTP is sent */}
            {otpSent && (
              <>
                <TextField
                  label="6-Digit Code"
                  type="text"
                  fullWidth
                  value={otp}
                  onChange={(e) => setOtp(e.target.value)}
                  required
                />
                <TextField
                  label="New Password"
                  type="password"
                  fullWidth
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </>
            )}

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
              disabled={disabled}
            >
              {otpSent ? "Continue" : "Reset Password"}
            </Button>
          </Stack>
        </form>
      </Paper>
    </Box>
  );
}
