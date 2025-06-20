'use client';

import { useState } from 'react';
import dynamic from 'next/dynamic';
import { Box, Container, Paper, Typography, Button } from '@mui/material';
import HintSidebar from '@/components/HintSidebar';
import ProblemStatement from '@/components/ProblemStatement';
import { getHint } from '@/services/api';

// Dynamically import Monaco Editor with no SSR
const MonacoEditor = dynamic(
  () => import('@monaco-editor/react').then((mod) => mod.default),
  { ssr: false }
);

export default function Home() {
  const [code, setCode] = useState<string>('');
  const [problemStatement, setProblemStatement] = useState<string>('');
  const [hints, setHints] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const handleEditorChange = (value: string | undefined) => {
    if (value !== undefined) {
      setCode(value);
    }
  };

  const handleGetHint = async () => {
    if (!problemStatement) {
      alert('Please enter a problem statement first!');
      return;
    }

    setLoading(true);
    try {
      // Create a timezone-naive date in ISO format
      const timestamp = new Date().toISOString();
      
      const response = await getHint({
        problem_statement: problemStatement,
        current_code: code,
        timestamp,
        previous_hints: hints
      });

      setHints([...hints, response.hint]);
    } catch (error) {
      console.error('Error getting hint:', error);
      alert('Failed to get hint. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-4">
      <Container maxWidth="xl" sx={{ height: '100vh', py: 2 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Contextual Hint Generation System
        </Typography>

        <Box sx={{ display: 'flex', gap: 2, height: 'calc(100% - 100px)' }}>
          <Box sx={{ flex: 3, display: 'flex', flexDirection: 'column', gap: 2 }}>
            <ProblemStatement
              value={problemStatement}
              onChange={(value) => setProblemStatement(value)}
            />
            
            <Paper elevation={3} sx={{ flex: 1, overflow: 'hidden' }}>
              <MonacoEditor
                height="100%"
                defaultLanguage="javascript"
                value={code}
                onChange={handleEditorChange}
                theme="vs-dark"
                options={{
                  minimap: { enabled: false },
                  fontSize: 14,
                  wordWrap: 'on'
                }}
                loading={<div>Loading editor...</div>}
              />
            </Paper>

            <Button
              variant="contained"
              color="primary"
              onClick={handleGetHint}
              disabled={loading}
              sx={{ alignSelf: 'flex-end' }}
            >
              {loading ? 'Getting Hint...' : 'Get Hint'}
            </Button>
          </Box>

          <HintSidebar hints={hints} />
        </Box>
      </Container>
    </main>
  );
} 