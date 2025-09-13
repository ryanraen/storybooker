import { Button } from "@mui/material";
import { useNavigate } from "react-router";

export default function LogoutButton() {
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            const res = await fetch("https://storybooker-api.vercel.app/user/logout", {
                method: "POST",
            });

            if (!res.ok) throw new Error("Logout failed");
            localStorage.removeItem("token");

            navigate("/login", {
                state: { successMessage: "Logged out successfully." },
            });
        } catch (err) {
            console.log(err.message);
        }

    };

    return (
        <Button
            onClick={handleLogout}
            variant="outlined"
            sx={{
                ml: "auto",
                borderRadius: 2,
                textTransform: "none",
                borderColor: "#e5e7eb",
                py: 1.4,
                fontSize: "1rem",
                "&:hover": {
                    borderColor: "#d1d5db",
                    bgcolor: "#f9fafb",
                },
            }}
        >
            Logout
        </Button>
    );
}
