import fetchMock from 'jest-fetch-mock';

fetchMock.enableMocks();

// Set up environment variables for tests
// We cast process.env to any to bypass the readonly TypeScript error,
// as we are intentionally modifying it for the test environment.
(process.env as any).NEXT_PUBLIC_API_BASE_URL = 'http://api.test.com';