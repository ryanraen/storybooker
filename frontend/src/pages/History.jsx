import { useState, useEffect } from "react";
import {
  Typography,
  Paper,
  List,
  ListItem,
  ListItemText,
  Button,
  IconButton,
} from "@mui/material";
import DownloadIcon from "@mui/icons-material/Download";

import DeleteButton from "../components/DeleteButton";

export default function HistoryPage() {
  const [historyItems, setHistoryItems] = useState([]);
  const [error, setError] = useState("");

  const downloadHref = (item) => {
    return `${import.meta.env.PROD ? import.meta.env.VITE_PROD_API_URL : import.meta.env.VITE_DEV_API_URL}/book/download?access_token=${localStorage.getItem("token")}&storybook_id=${item.id}`;
  };

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await fetch(
          `${import.meta.env.PROD ? import.meta.env.VITE_PROD_API_URL : import.meta.env.VITE_DEV_API_URL}/get-history`,
          {
            method: "GET",
            headers: {
              "Content-Type": "image/png",
              "Content-Disposition": "attachment",
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        );

        if (!res.ok) throw new Error("Failed to fetch history");

        const data = await res.json();
        setHistoryItems(data.history);
      } catch (err) {
        setError("Could not load history");
        console.log(err.message);
      }
    };
    fetchHistory();
  }, []);

  return (
    <Paper
      sx={{
        p: 5,
        borderRadius: 3,
        boxShadow: 2,
        width: "100%",
        maxWidth: "100%",
        bgcolor: "white",
        position: "relative",
        zIndex: 2,
      }}
    >
      <Typography variant="h5" fontWeight="bold" gutterBottom>
        History
      </Typography>
      <Typography color="text.secondary" gutterBottom>
        Previously generated storybooks.
      </Typography>
      <List sx={{ mt: 2 }}>
        {historyItems.map((item) => (
          <ListItem
            key={item.id}
            sx={{
              borderRadius: 2,
              mb: 1,
              "&:hover": { bgcolor: "#f9fafb" },
            }}
          >
            <ListItemText
              primary={item.title}
              secondary={new Date(item.date.slice(0, 10)).toLocaleDateString(
                "en-US",
                { year: "numeric", month: "long", day: "numeric" }
              )}
            />

            <IconButton
              href={downloadHref(item)}
              size="large"
              aria-label="Download"
              sx={{
                bgcolor: "#EEE",
                "&:hover": { bgcolor: "#AAA" },
                textTransform: "none",
                borderRadius: 2,
                py: 1.2,
                px: 1.2,
              }}
            >
              <DownloadIcon />
            </IconButton>

            <DeleteButton item={item} />
          </ListItem>
        ))}
      </List>
      {error && (
        <Typography color="error" fontSize="0.9rem">
          {error}
        </Typography>
      )}
    </Paper>
  );
}
