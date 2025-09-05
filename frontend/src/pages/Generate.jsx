import { Typography, Paper, Button, Stack, TextField } from "@mui/material";

export default function Generate() {
  return (
    <Paper
      sx={{
        p: 5,
        borderRadius: 3,
        boxShadow: 2,
        bgcolor: "white",
      }}
    >
      <Typography variant="h5" fontWeight="bold" gutterBottom>
        Generate a Storybook
      </Typography>
      <Typography color="text.secondary" gutterBottom>
        Enter your idea and generate a custom storybook instantly.
      </Typography>

      <Stack spacing={3} mt={3}>
        <TextField
          label="Story Idea"
          placeholder="e.g. A dragon learns about honesty"
          fullWidth
          variant="outlined"
        />
        <Button
          variant="contained"
          sx={{
            bgcolor: "black",
            "&:hover": { bgcolor: "#111" },
            textTransform: "none",
            borderRadius: 2,
            py: 1.2,
          }}
        >
          Generate
        </Button>
      </Stack>
    </Paper>
  );
}
