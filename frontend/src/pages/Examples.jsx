import React from "react";
import { Box, Typography, Grid, Card, CardMedia, CardContent, Button } from "@mui/material";

const examples = [
    // placeholders
    {
        title: "The Brave Bunny",
        description: "A little bunny who overcomes fears and discovers bravery on her first day of school.",
        image: "/storybook-preview.png",
    },
    // {
    //     title: "The Honest Dragon",
    //     description: "A dragon who learns the value of honesty through magical adventures.",
    //     image: "/examples/honest-dragon.png",
    // },
    // {
    //     title: "Luna’s Space Journey",
    //     description: "Follow Luna as she travels across the stars to make new friends.",
    //     image: "/examples/luna-space.png",
    // },
    // {
    //     title: "The Brave Little Fox",
    //     description: "A story about courage, kindness, and helping others in the forest.",
    //     image: "/examples/brave-fox.png",
    // },
    // {
    //     title: "The Lost Pirate Treasure",
    //     description: "Pirates and children team up to discover the true treasure: friendship.",
    //     image: "/examples/pirate-treasure.png",
    // },
];

export default function SeeExamples() {
    return (
        <Box sx={{ py: 8, px: { xs: 2, md: 8 } }}>
            <Box sx={{ textAlign: "center", mb: 6 }}>
                <Typography variant="h3" fontWeight="bold" gutterBottom>
                    See Example Storybooks
                </Typography>
                <Typography variant="h6" color="text.secondary">
                    Browse through some of the magical storybooks our agent can create from just one idea.
                </Typography>
            </Box>

            <Grid container spacing={4}>
                {examples.map((example, index) => (
                    <Grid item xs={12} sm={6} md={3} key={index}>
                        <Card
                            sx={{
                                borderRadius: "20px",
                                boxShadow: 3,
                                height: "100%",
                                display: "flex",
                                flexDirection: "column",
                            }}
                        >
                            <CardMedia
                                component="img"
                                image={example.image}
                                alt={example.title}
                                sx={{ borderTopLeftRadius: "20px", borderTopRightRadius: "20px", height: 420, }}
                            />
                            <CardContent sx={{ flexGrow: 1 }}>
                                <Typography variant="h6" fontWeight="bold">
                                    {example.title}
                                </Typography>
                                <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                                    {example.description}
                                </Typography>
                            </CardContent>
                        </Card>
                    </Grid>
                ))}
            </Grid>

            <Box sx={{ textAlign: "center", mt: 8 }}>
                <Button
                    variant="contained"
                    color="primary"
                    size="large"
                    sx={{ borderRadius: "12px", px: 4, py: 1.5 }}
                    href="/dashboard/generate"
                >
                    Create Your Own Storybook
                </Button>
            </Box>
        </Box>
    );
}
