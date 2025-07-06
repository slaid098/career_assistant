import { Job } from './jobService.types';

const getApiUrl = (): string => {
    const url = process.env.NEXT_PUBLIC_API_URL;
    if (!url) {
        throw new Error('NEXT_PUBLIC_API_URL is not defined');
    }
    return url;
};

const mockJobs: Job[] = [
    {
        id: 1,
        title: 'Frontend Developer (React)',
        company: 'Meta',
        url: '#',
        created_at: new Date().toISOString(),
        description: 'We are looking for a talented Frontend Developer to join our team. You will be responsible for building the next generation of our user interfaces.',
    },
    {
        id: 2,
        title: 'Fullstack Engineer',
        company: 'Google',
        url: '#',
        created_at: new Date(Date.now() - 86400000 * 2).toISOString(), // 2 days ago
        description: 'Join our team to work on exciting new projects that reach millions of users. Strong experience with Node.js and React is required.',
    },
    {
        id: 3,
        title: 'TypeScript Developer',
        company: 'Microsoft',
        url: '#',
        created_at: new Date(Date.now() - 86400000 * 5).toISOString(), // 5 days ago
        description: 'Are you passionate about TypeScript? We are looking for an expert to help us build robust and scalable applications.',
    },
];

const validateResponse = async <T>(response: Response): Promise<T> => {
    if (!response.ok) {
        const errorText = await response.text();
        console.error('API Error:', errorText);
        throw new Error(`Network response was not ok: ${response.statusText}`);
    }
    return response.json() as Promise<T>;
};

export const getJobs = async (): Promise<Job[]> => {
    const getJobUrl = `${getApiUrl()}/jobs`;
    try {
        const response = await fetch(getJobUrl);
        return validateResponse<Job[]>(response);
    } catch (error) {
        console.warn('Could not fetch jobs from backend, returning mock data.', error);
        return mockJobs;
    }
};

export const getJobById = async (id: string): Promise<Job | null> => {
    const getJobUrl = `${getApiUrl()}/jobs/${id}`;
    try {
        const response = await fetch(getJobUrl);
        if (response.status === 404) {
            return null; // Explicitly handle 404 Not Found
        }
        return validateResponse<Job>(response);
    } catch (error) {
        console.warn(`Could not fetch job ${id} from backend, returning mock data.`, error);
        const job = mockJobs.find((j) => j.id.toString() === id) || null;
        return job;
    }
};





