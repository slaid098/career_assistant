import { getJobs, getJobById } from '@/services/jobService';
import { Job } from '@/services/jobService.types';
import fetchMock from 'jest-fetch-mock';

describe('jobService', () => {
  beforeEach(() => {
    fetchMock.resetMocks();
  });

  it('should fetch and return a list of jobs', async () => {
    const mockJobs: Job[] = [
      {
        id: 1,
        title: 'Python Developer',
        url: 'http://example.com/job/1',
        company: 'Example Corp',
        created_at: new Date().toISOString(),
        description: 'A great job for a Python expert.',
      },
      {
        id: 2,
        title: 'Frontend Developer',
        url: 'http://example.com/job/2',
        company: 'Another Corp',
        created_at: new Date().toISOString(),
        description: 'A great job for a React expert.',
      },
    ];

    fetchMock.mockResponseOnce(JSON.stringify(mockJobs));

    const jobs = await getJobs();

    expect(fetchMock.mock.calls.length).toBe(1);
    const expectedUrl = new URL('/jobs', process.env.NEXT_PUBLIC_API_BASE_URL!).toString();
    expect(fetchMock.mock.calls[0][0]).toBe(expectedUrl);

    expect(jobs).toEqual(mockJobs);
  });

  it('should fetch a single job by id', async () => {
    const mockJob: Job = {
        id: 1,
        title: 'Python Developer',
        url: 'http://example.com/job/1',
        company: 'Example Corp',
        created_at: new Date().toISOString(),
        description: 'A great job for a Python expert.',
    };
    fetchMock.mockResponseOnce(JSON.stringify(mockJob));

    const job = await getJobById('1');

    const expectedUrl = new URL('/jobs/1', process.env.NEXT_PUBLIC_API_BASE_URL!).toString();
    expect(fetchMock.mock.calls[0][0]).toBe(expectedUrl);
    expect(job).toEqual(mockJob);
  });

  it('should return null when a job is not found (404)', async () => {
    fetchMock.mockResponseOnce('', { status: 404 });

    const job = await getJobById('999');

    const expectedUrl = new URL('/jobs/999', process.env.NEXT_PUBLIC_API_BASE_URL!).toString();
    expect(fetchMock.mock.calls[0][0]).toBe(expectedUrl);
    expect(job).toBeNull();
  });
});