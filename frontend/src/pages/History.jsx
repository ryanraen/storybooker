import { useState, useEffect } from 'react';
import { Typography, Paper, List, ListItem, ListItemText, Button, IconButton } from "@mui/material";
import DownloadIcon from '@mui/icons-material/Download';

export default function HistoryPage() {

  const [historyItems, setHistoryItems] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await fetch("https://storybooker-api.vercel.app/get-history", {
          method: "GET",
          headers: {
            "Content-Type": "image/png",
            "Content-Disposition": "attachment",
            "Authorization": `Bearer ${localStorage.getItem("token")}`
          },
        });

        if (!res.ok) throw new Error("Failed to fetch history");

        const data = await res.json();
        setHistoryItems(data.history);
      } catch (err) {
        setError("Could not load history");
        console.log(err.message);
      }
    };
    fetchHistory();
  })

  const handleDownload = async (id) => {
    setError("");

    try {
      const res = await fetch("https://storybooker-api.vercel.app/download?storybook_id=" + id, {
        method: "GET",
        headers: { "Content-Type": "application/json", "Authorization": `Bearer ${localStorage.getItem("token")}` },
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error);

      return (data.pdf_data);
    } catch (err) {
      setError("Unable to download storybook");
      console.log(err.message);
    }
  }

  return (
    <Paper sx={{ p: 5, borderRadius: 3, boxShadow: 2, bgcolor: "white" }}>
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
              secondary={new Date(item.date.slice(0, 10)).toLocaleDateString("en-US", { year: 'numeric', month: 'long', day: 'numeric' })}
            />

            <IconButton
              href={`https://storybooker-api.vercel.app/download?access_token=${localStorage.getItem("token")}&storybook_id=${item.id}`}
              color="inherit"
              size="large"
              sx={{
                bgcolor: "#EEE",
                "&:hover": { bgcolor: "#AAA" },
                textTransform: "none",
                borderRadius: 2,
                py: 1.2,
              }}
            >
              <DownloadIcon />
            </IconButton>
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
