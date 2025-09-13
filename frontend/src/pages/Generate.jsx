import { useState } from "react";
import { Typography, Paper, Button, Stack, TextField } from "@mui/material";

export default function Generate() {

  const [title, setTitle] = useState("");
  const [prompt, setPrompt] = useState("");
  const [error, setError] = useState("");
  const [pdf, setPdf] = useState("");

  const handleGenerate = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await fetch("http://localhost:5000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json", "Authorization": `Bearer ${localStorage.getItem("token")}` },
        body: JSON.stringify({ title, prompt }),
      });

      if (!res.ok) throw new Error("Generation failed");

      const data = await res.json()
      setPdf(data.pdf_data);
    } catch (err) {
      setError("Generation request failed");
      console.log(err.message);
    }
  };

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

      <form onSubmit={handleGenerate}>
        <Stack spacing={3} mt={3}>
          <TextField
            label="Title"
            placeholder="e.g. Tale of the Truthful Dragon"
            fullWidth
            onChange={(e) => setTitle(e.target.value)}
            variant="outlined"
          />
          <TextField
            label="Story Idea"
            placeholder="e.g. A dragon learns about honesty"
            fullWidth
            onChange={(e) => setPrompt(e.target.value)}
            variant="outlined"
          />
          <Button
            type="submit"
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
          {error && (
            <Typography color="error" fontSize="0.9rem">
              {error}
            </Typography>
          )}
        </Stack>
        {pdf && (
          <embed
            src={`data:application/pdf;base64,${pdf}`}
            type="application/pdf"
            width="100%"
            height="600px"
            style={{ marginTop: "20px", borderRadius: "8px", boxShadow: "0 2px 8px rgba(0, 0, 0, 0.1)" }}
          />
        )}
      </form>
    </Paper>
  );
}
