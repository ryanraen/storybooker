import { Button } from "@mui/material";
import { useNavigate } from "react-router";

export default function LogoutButton() {
    const navigate = useNavigate();

    const handleLogout = () => {
        const res = fetch("http://localhost:5000/user/logout", {
            method: "POST",
        });

        if (!res.ok) throw new Error("Logout failed");
        localStorage.removeItem("token");

        navigate("/login");
    };

    return (
        <Button
            onClick={handleLogout}
            variant="outlined"
            sx={{
                ml: "auto",
                borderRadius: 2,
                textTransform: "none",
                // bgcolor: "black",
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
