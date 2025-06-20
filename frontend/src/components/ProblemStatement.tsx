import React from 'react';
import { Paper, TextField } from '@mui/material';

interface ProblemStatementProps {
  value: string;
  onChange: (value: string) => void;
}

const ProblemStatement: React.FC<ProblemStatementProps> = ({ value, onChange }) => {
  return (
    <Paper elevation={3} sx={{ p: 2 }}>
      <TextField
        fullWidth
        multiline
        rows={4}
        label="Problem Statement"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Enter your programming problem here..."
        variant="outlined"
      />
    </Paper>
  );
};

export default ProblemStatement; 