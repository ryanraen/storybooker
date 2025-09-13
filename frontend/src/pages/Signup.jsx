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
import { useNavigate } from "react-router";

export default function Signup() {
    const navigate = useNavigate();

    // form state
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleSignup = async (e) => {
        e.preventDefault();
        setError("");

        try {
            const res = await fetch("https://storybooker-api.vercel.app/user/signup", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, username, password }),
            });

            if (!res.ok) throw new Error("Signup failed");

            const data = await res.json();
            navigate("/login");
        } catch (err) {
            setError("Unable to create account");
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
                    Create Account
                </Typography>
                <Typography color="text.secondary" mb={3}>
                    Start your journey by creating a new account.
                </Typography>

                <form onSubmit={handleSignup}>
                    <Stack spacing={3}>
                        <TextField
                            label="Name"
                            fullWidth
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            variant="outlined"
                            required
                        />
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
                            Sign up
                        </Button>

                        <Stack direction="row" justifyContent="center" mt={1}>
                            <Typography variant="body2" color="text.secondary">
                                Already have an account?{" "}
                                <Link href="/login" underline="hover">
                                    Sign in
                                </Link>
                            </Typography>
                        </Stack>
                    </Stack>
                </form>
            </Paper>
        </Box>
    );
}
