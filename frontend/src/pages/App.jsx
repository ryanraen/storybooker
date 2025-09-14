import {
  Box,
  Container,
  Typography,
  Button,
  Card,
  CardContent,
  AppBar,
  Toolbar,
  Grid,
  CardMedia,
} from "@mui/material";
import { Book, AutoStories, AutoFixHigh } from "@mui/icons-material";

export default function App() {
  const features = [
    {
      icon: <Book sx={{ fontSize: 40, color: "#3f51b5" }} />,
      title: "Infinite Storybooks",
      desc: "Generate unlimited storybooks tailored to every child’s needs and interests.",
    },
    {
      icon: <AutoStories sx={{ fontSize: 40, color: "#3f51b5" }} />,
      title: "Interactive Characters",
      desc: "Bring your child’s favorite characters into customized stories that teach valuable lessons.",
    },
    {
      icon: <AutoFixHigh sx={{ fontSize: 40, color: "#3f51b5" }} />,
      title: "Fully Customizable",
      desc: "Adjust plots, settings, and morals to fit each child’s personality and developmental needs.",
    },
  ];

  const steps = [
    {
      title: "Enter a Scenario",
      desc: "Describe a situation or moral you want to teach, like honesty or kindness.",
    },
    {
      title: "Personalize the Story",
      desc: "Choose favorite characters, settings, and other elements that resonate with your child.",
    },
    {
      title: "Generate & Share",
      desc: "Get an interactive storybook instantly, ready to read, share, or print.",
    },
  ];

  const examples = [
    // placeholders
    {
      title: "The Truthful Dragon",
      description:
        "A dragon who learns the value of honesty through magical adventures.",
      image: "/dragon_demo.png",
    },
    {
      title: "The Brave Bunny",
      description:
        "A little bunny who overcomes fears and discovers bravery on her first day of school.",
      image: "/bunny_demo.png",
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

  return (
    <Box
      sx={{
        position: "relative",
        minHeight: "100vh",
        overflow: "hidden",
      }}
    >
      {/* Fixed Background */}
      <Box
        sx={{
          position: "fixed",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          backgroundImage: "url('/storybooker-background.png')",
          backgroundSize: "cover",
          backgroundPosition: "center",
          filter: "blur(8px)",
          transform: "scale(1.1)",
          zIndex: -2,
        }}
      />

      <Box
        sx={{
          position: "fixed",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          bgcolor: "rgba(255,255,255,0.6)",
          zIndex: -1,
        }}
      />

      <Box>
        {/* Header */}
        <AppBar position="static" color="secondary" elevation={0}>
          <Toolbar sx={{ justifyContent: "space-between" }}>
            <Typography variant="h6" sx={{ fontWeight: "bold" }}>
              Storybooker
            </Typography>
            <Box>
              {["Features", "How It Works", "Get Started"].map((item) => (
                <Button
                  key={item}
                  color="inherit"
                  href={
                    item === "Get Started"
                      ? "/login"
                      : "#" + item.toLowerCase().replace(/ /g, "-")
                  }
                >
                  {item}
                </Button>
              ))}
            </Box>
          </Toolbar>
        </AppBar>

        {/* Hero */}
        <Container
          maxWidth="lg"
          sx={{
            py: 10,
            display: "flex",
            flexDirection: { xs: "column", md: "row" },
            alignItems: "center",
            gap: 5,
          }}
        >
          <Box flex={1}>
            <Typography variant="h3" fontWeight="bold" gutterBottom>
              Infinite, Interactive Storybooks <br />{" "}
              <span style={{ color: "#3f51b5" }}>Tailored for Every Child</span>
            </Typography>
            <Typography variant="body1" color="text.secondary" mb={3}>
              Storybooker lets you create storybooks that adapt to your child’s
              interests, behaviors, and developmental needs. From teaching
              morals to encouraging creativity, every story is a unique
              experience.
            </Typography>
            <Box sx={{ display: "flex", gap: 2 }}>
              <Button variant="contained" size="large" href="/login">
                Create Your Storybook
              </Button>
              <Button variant="outlined" size="large" href="/examples">
                See Examples
              </Button>
            </Box>
          </Box>
          <Box flex={1}>
            <img
              src="/dragon_demo.png"
              alt="Storybook preview"
              style={{
                borderRadius: 16,
                width: "100%",
                boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
              }}
            />
            {/* alternate header image medium-shot-mother-holding-kid-laptop.jpg */}
          </Box>
        </Container>

        {/* Examples */}
        <Box sx={{ py: 8, px: { xs: 2, md: 8 } }}>
          <Box sx={{ textAlign: "center", mb: 6 }}>
            <Typography variant="h3" fontWeight="bold" gutterBottom>
              See Example Storybooks
            </Typography>
            <Typography variant="h6" color="text.secondary">
              Browse through some of the magical storybooks our AI agent can
              create from just one idea.
            </Typography>
          </Box>

          <Grid container spacing={4}>
            {examples.map((example, index) => (
              <Grid item xs={12} sm={6} md={3} key={index} margin="auto">
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
                    sx={{
                      borderTopLeftRadius: "20px",
                      borderTopRightRadius: "20px",
                      height: 420,
                    }}
                  />
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Typography variant="h6" fontWeight="bold">
                      {example.title}
                    </Typography>
                    <Typography
                      variant="body2"
                      color="text.secondary"
                      sx={{ mt: 1 }}
                    >
                      {example.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Features */}
        <Container maxWidth="lg" sx={{ py: 10 }} id="features">
          <Typography variant="h4" fontWeight="bold" textAlign="center" mb={5}>
            Why Storybooker?
          </Typography>
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              gap: 3,
              flexWrap: "nowrap",
            }}
          >
            {features.map((f, i) => (
              <Card
                key={i}
                sx={{
                  flex: "1 1 0",
                  textAlign: "center",
                  p: 3,
                  borderRadius: 3,
                  boxShadow: 3,
                }}
              >
                <CardContent>
                  {f.icon}
                  <Typography variant="h6" fontWeight="bold" mt={2}>
                    {f.title}
                  </Typography>
                  <Typography color="text.secondary" mt={1}>
                    {f.desc}
                  </Typography>
                </CardContent>
              </Card>
            ))}
          </Box>
        </Container>

        {/* How it works */}
        <Container maxWidth="md" sx={{ py: 10 }} id="how-it-works">
          <Typography variant="h4" fontWeight="bold" textAlign="center" mb={5}>
            How It Works
          </Typography>
          <Box component="ol" sx={{ pl: 3, "& li": { mb: 3 } }}>
            {steps.map((step, i) => (
              <Box component="li" key={i}>
                <Typography variant="h6" fontWeight="bold">
                  {step.title}
                </Typography>
                <Typography color="text.secondary">{step.desc}</Typography>
              </Box>
            ))}
          </Box>
        </Container>

        {/* Call to Action */}
        <Box
          sx={{
            py: 10,
            bgcolor: "#3f51b5",
            color: "#fff",
            textAlign: "center",
          }}
          id="cta"
        >
          <Typography variant="h4" fontWeight="bold" mb={2}>
            Make Every Story Unique
          </Typography>
          <Typography mb={4}>
            From teaching life lessons to sparking imagination, Storybooker lets
            you create an endless library of interactive, personalized stories.
          </Typography>
          <Button
            variant="contained"
            color="secondary"
            size="large"
            href="/login"
          >
            Start Creating Now
          </Button>
        </Box>

        {/* Footer */}
        <Box sx={{ py: 5, textAlign: "center", color: "text.secondary" }}>
          © {new Date().getFullYear()} Storybooker. No rights reserved.
        </Box>
      </Box>
    </Box>
  );
}
