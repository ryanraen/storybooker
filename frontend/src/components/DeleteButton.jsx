import { useState } from "react";
import {
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";

export default function DeleteButton({item}) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState();

  const handleClickOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  const handleConfirm = async () => {
    setLoading(true);

    try {
      const res = await fetch(
        `${import.meta.env.PROD ? import.meta.env.VITE_PROD_API_URL : import.meta.env.VITE_DEV_API_URL}/book/delete?access_token=${localStorage.getItem("token")}&storybook_id=${item.id}`,
        {
          method: "DELETE",
          headers: { "Content-Type": "application/json" },
        }
      );

      const data = await res.json();
      console.log(data.error);

      if (!res.ok) throw new Error("Failed to delete storybook");
      
    } catch (err) {
      setError("Failed to delete storybook");
      console.log(err.message);
    }

    setOpen(false);
    setLoading(false);
  };

  return (
    <>
      <IconButton
        variant="outlined"
        color="error"
        size="large"
        onClick={handleClickOpen}
        sx={{
          bgcolor: "#FEE",
          "&:hover": { bgcolor: "#FCC" },
          textTransform: "none",
          borderRadius: 2,
          py: 1.2,
          px: 1.2,
          marginLeft: 0.5,
        }}
      >
        <DeleteIcon />
      </IconButton>

      <Dialog open={open} onClose={handleClose}>
        <DialogTitle sx={{ fontWeight: 700 }}>Delete Item?</DialogTitle>
        <DialogContent>
          <DialogContentText sx={{ color: "text.secondary" }}>
            This action cannot be undone. Are you sure you want to delete this?
          </DialogContentText>
        </DialogContent>
        <DialogActions sx={{ px: 3, pb: 2 }}>
          <Button
            onClick={handleClose}
            sx={{ textTransform: "none", borderRadius: 2 }}
            disabled={loading}
          >
            Cancel
          </Button>
          <Button
            onClick={handleConfirm}
            variant="contained"
            color="error"
            sx={{ textTransform: "none", borderRadius: 2, fontWeight: 600 }}
            loading={loading}
          >
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
