import { useState } from "react";
import { Button } from "@mui/material";
import { useNavigate } from "react-router";

export default function LogoutButton() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleLogout = async () => {
    setLoading(true);
    try {
      const res = await fetch(
        `${import.meta.env.PROD ? import.meta.env.VITE_PROD_API_URL : import.meta.env.VITE_DEV_API_URL}/user/logout`,
        {
          method: "POST",
        }
      );

      if (!res.ok) throw new Error("Logout failed");
      localStorage.removeItem("token");

      navigate("/login", {
        state: { successMessage: "Logged out successfully." },
      });
    } catch (err) {
      console.log(err.message);
    }
    setLoading(false);
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
      loading={loading}
    >
      Logout
    </Button>
  );
}
