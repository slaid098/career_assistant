import { Job } from '@/services/jobService.types'


/**
 * Verifies if the provided API URL is defined.
 * Throws an error if the URL is undefined, indicating a configuration issue.
 *
 * Args:
 *   apiUrl: The API base URL, which can be a string or undefined.
 *
 * Throws:
 *   Error: If the API base URL is not configured.
 */
const verifyApiUrl = (apiUrl: string | undefined): void => {
    if (!apiUrl) {
        throw new Error("API base URL is not configured. Please check your .env.local file.")
    }
}

/**
 * Retrieves and validates the API base URL from environment variables.
 * This function ensures that the API URL is always available and properly configured
 * before making API calls.
 *
 * Returns:
 *   string: The validated API base URL.
 *
 * Throws:
 *   Error: If the API base URL is not configured.
 */
const getApiUrl = (): string => {
    const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL
    verifyApiUrl(apiUrl)
    return apiUrl
}

/**
 * Validates the HTTP response from an API call.
 * If the response is not OK (status code not in 200-299 range), it throws an error
 * with details from the response body. Otherwise, it parses and returns the JSON body.
 *
 * Args:
 *   response: The Fetch API Response object to validate.
 *
 * Returns:
 *   Promise<T>: A promise that resolves with the parsed JSON body of type T.
 *
 * Throws:
 *   Error: If the response status is not OK.
 */
const validateResponse = async <T>(response: Response): Promise<T> => {
    if (!response.ok) {
        const errorBody = await response.text() // Переименовали для ясности
        throw new Error(`Request failed. Status: ${response.status}, Body: ${errorBody}`)
    }
    return response.json() as T
}

/**
 * Fetches a list of jobs from the API.
 * This function constructs the API endpoint for jobs and handles the network request,
 * including validation of the response.
 *
 * Returns:
 *   Promise<Job[]>: A promise that resolves with an array of Job objects.
 *
 * Throws:
 *   Error: If the API call fails or the response is not OK.
 */
export const getJobs = async (): Promise<Job[]> => {
    const apiUrl = getApiUrl()
    const getJobUrl = new URL("/jobs", apiUrl).toString()
    const response = await fetch(getJobUrl)
    return validateResponse<Job[]>(response) // Указываем ожидаемый тип Job[]
}

/**
 * Fetches a single job by its ID from the API.
 * This function constructs the API endpoint for a specific job and handles
 * the network request, including validation and handling of 404 Not Found responses.
 *
 * Args:
 *   id: The unique identifier of the job to fetch.
 *
 * Returns:
 *   Promise<Job | null>: A promise that resolves with a Job object if found,
 *                       or null if the job is not found (404 status).
 *
 * Throws:
 *   Error: If the API call fails with a status other than 404, or the response is not OK.
 */
export const getJobById = async (id: string): Promise<Job | null> => {
    const apiUrl = getApiUrl();
    const getJobUrl = new URL(`/jobs/${id}`, apiUrl).toString();
    const response = await fetch(getJobUrl);

    if (response.status === 404) {
        return null;
    }

    return validateResponse<Job>(response);
};





