import { useState } from "react";
import {
    Box,
    Paper,
    Typography,
    TextField,
    Button,
    Stack,
    Link,
} from "@mui/material";
import { useNavigate, useLocation } from "react-router";

export default function Login() {
    const navigate = useNavigate();
    const location = useLocation();
    const successMessage = location.state?.successMessage;

    // Form state
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLogin = async (e) => {
        e.preventDefault();
        setError("");

        try {
            const res = await fetch("https://storybooker-api.vercel.app/user/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });

            if (!res.ok) throw new Error("Login failed");

            const data = await res.json();
            localStorage.setItem("token", data.session.access_token);
            navigate("/dashboard");
        } catch (err) {
            setError("Invalid email or password");
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
            <Paper
                sx={{
                    p: 5,
                    borderRadius: 3,
                    boxShadow: 3,
                    width: "100%",
                    maxWidth: 420,
                    bgcolor: "white",
                }}
            >
                <Typography variant="h5" fontWeight="bold" gutterBottom>
                    Log in
                </Typography>
                <Typography color="text.secondary" mb={3}>
                    Continue to Storybooker
                </Typography>

                <form onSubmit={handleLogin}>
                    <Stack spacing={3}>
                        <TextField
                            label="Email"
                            type="email"
                            fullWidth
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            variant="outlined"
                            required
                        />
                        <TextField
                            label="Password"
                            type="password"
                            fullWidth
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            variant="outlined"
                            required
                        />

                        {successMessage && (
                            <Typography
                                sx={{
                                    mb: 2,
                                    px: 3,
                                    py: 1.5,
                                    borderRadius: 2,
                                    bgcolor: "#d1fae5",
                                    color: "#065f46",
                                    fontWeight: 500,
                                }}
                            >
                                {successMessage}
                            </Typography>
                        )}

                        {error && (
                            <Typography color="error" fontSize="0.9rem">
                                {error}
                            </Typography>
                        )}

                        <Button
                            type="submit"
                            variant="contained"
                            fullWidth
                            sx={{
                                bgcolor: "black",
                                "&:hover": { bgcolor: "#111" },
                                textTransform: "none",
                                borderRadius: 2,
                                py: 1.4,
                                fontSize: "1rem",
                            }}
                        >
                            Sign in
                        </Button>

                        <Stack direction="row" justifyContent="space-between" mt={1}>
                            <Link href="/forgot-password" variant="body2" underline="hover">
                                Forgot password?
                            </Link>
                            <Link href="/signup" variant="body2" underline="hover">
                                Create account
                            </Link>
                        </Stack>
                    </Stack>
                </form>
            </Paper>
        </Box>
    );
}
