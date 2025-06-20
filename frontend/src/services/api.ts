import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export interface HintRequest {
  problem_statement: string;
  current_code: string;
  timestamp: string;
  previous_hints: string[];
}

export interface HintResponse {
  hint: string;
  hint_type: string;
}

export const getHint = async (request: HintRequest): Promise<HintResponse> => {
  const response = await axios.post<HintResponse>(`${API_BASE_URL}/hint`, request);
  return response.data;
}; 