import { Typography, Paper, List, ListItem, ListItemText } from "@mui/material";

const historyItems = [
// eg. { id: 1, title: "The Honest Dragon", date: "Aug 20, 2025" }, 
];

export default function HistoryPage() {
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
              secondary={item.date}
              primaryTypographyProps={{ fontWeight: 500 }}
            />
          </ListItem>
        ))}
      </List>
    </Paper>
  );
}
