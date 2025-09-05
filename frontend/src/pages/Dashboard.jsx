import { Routes, Route, Link, useLocation } from "react-router";
import {
  Box,
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  AppBar,
  Typography,
  Paper,
} from "@mui/material";
import { AutoAwesome, History } from "@mui/icons-material";
import Generate from "./Generate";
import HistoryPage from "./History";

const drawerWidth = 240;

export default function Dashboard() {
  const location = useLocation();

  const navItems = [
    { text: "Generate", icon: <AutoAwesome />, path: "generate" },
    { text: "History", icon: <History />, path: "history" },
  ];

  return (
    <Box sx={{ display: "flex", bgcolor: "#f9fafb", minHeight: "100vh" }}>
      {/* Top AppBar */}
      <AppBar
        position="fixed"
        elevation={0}
        sx={{
          bgcolor: "white",
          borderBottom: "1px solid #e5e7eb",
          zIndex: (theme) => theme.zIndex.drawer + 1,
        }}
      >
        <Toolbar>
          <Typography variant="h6" color="text.primary" fontWeight="bold">
            Dashboard
          </Typography>
        </Toolbar>
      </AppBar>

      {/* Sidebar Drawer */}
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: {
            width: drawerWidth,
            boxSizing: "border-box",
            borderRight: "1px solid #e5e7eb",
            bgcolor: "white",
          },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: "auto", mt: 2 }}>
          <List>
            {navItems.map((item) => (
              <ListItemButton
                key={item.text}
                component={Link}
                to={item.path}
                selected={location.pathname.includes(item.path)}
                sx={{
                  borderRadius: 2,
                  mx: 1,
                  mb: 1,
                  "&.Mui-selected": {
                    bgcolor: "#f3f4f6",
                  },
                  "&:hover": {
                    bgcolor: "#f9fafb",
                  },
                }}
              >
                <ListItemIcon sx={{ minWidth: 40, color: "text.secondary" }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText primary={item.text} primaryTypographyProps={{ fontWeight: 500 }} />
              </ListItemButton>
            ))}
          </List>
        </Box>
      </Drawer>

      {/* Main Content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 4,
          mt: 8,
        }}
      >
        <Routes>
          <Route path="generate" element={<Generate />} />
          <Route path="history" element={<HistoryPage />} />
          <Route
            path="*"
            element={
              <Paper sx={{ p: 5, borderRadius: 3, boxShadow: 2 }}>
                <Typography variant="h5" fontWeight="bold" gutterBottom>
                  Welcome to the Dashboard
                </Typography>
                <Typography color="text.secondary">
                  Select a section from the sidebar to get started.
                </Typography>
              </Paper>
            }
          />
        </Routes>
      </Box>
    </Box>
  );
}
