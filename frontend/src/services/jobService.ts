import { Job } from '@/services/jobService.types';


export const getJobs = async (): Promise<Job[]> => {
    const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL

    if (!apiUrl) {
        throw new Error("API base URL is not configured. Please check your .env.local file.");
    }

    const getJobUrl = new URL("/jobs", apiUrl)
    const response = await fetch(getJobUrl.toString())
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to get jobs. Status: ${response.status}, Body: ${errorText}`)
    };
    return response.json();
}
