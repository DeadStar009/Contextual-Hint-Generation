import React from 'react';
import { Paper, Typography, Box } from '@mui/material';

interface HintSidebarProps {
  hints: string[];
}

const HintSidebar: React.FC<HintSidebarProps> = ({ hints }) => {
  return (
    <Paper
      elevation={3}
      sx={{
        flex: 1,
        p: 2,
        backgroundColor: '#f5f5f5',
        overflowY: 'auto',
        height: '100%'
      }}
    >
      <Typography variant="h6" gutterBottom>
        Hints History
      </Typography>

      {hints.length === 0 ? (
        <Typography color="text.secondary" sx={{ fontStyle: 'italic' }}>
          No hints requested yet. Click "Get Hint" when you need help!
        </Typography>
      ) : (
        hints.map((hint, index) => (
          <Box
            key={index}
            sx={{
              mb: 2,
              p: 2,
              backgroundColor: 'white',
              borderRadius: 1,
              boxShadow: 1
            }}
          >
            <Typography variant="subtitle2" color="text.secondary" gutterBottom>
              Hint #{index + 1}
            </Typography>
            <Typography>{hint}</Typography>
          </Box>
        ))
      )}
    </Paper>
  );
};

export default HintSidebar; 