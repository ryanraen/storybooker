import { createTheme } from '@mui/material/styles';
import { red } from '@mui/material/colors';

const homeTheme = createTheme({
  cssVariables: true,
  palette: {
    primary: {
      main: '#556cd6',
    },
    secondary: {
      main: '#ffffff',
    },
    error: {
      main: red.A400,
    },
  },
});

export default homeTheme;
