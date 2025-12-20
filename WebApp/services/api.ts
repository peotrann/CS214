
import { LawResult } from '../types';

/**
 * Since the user's logic is in Python (D:\CS214\Engine),
 * this React app expects a REST API running on localhost.
 * The user would typically run a FastAPI/Flask server that imports '07_web_api.py'.
 */

const API_BASE_URL = 'http://localhost:8000';

export const queryTrafficLaw = async (query: string): Promise<LawResult[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    return data.results as LawResult[];
  } catch (error) {
    console.error('Error fetching laws:', error);
    // In a real scenario, we might want to return mock data for demo purposes 
    // but the prompt says "do not create new data". 
    // We will assume the local server is reachable.
    throw error;
  }
};
