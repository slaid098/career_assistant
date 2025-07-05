import { getJobById } from '@/services/jobService';
import { Job } from '@/services/jobService.types';

interface JobDetailPageProps {
    params: {
        jobId: string;
    };
}
export const jobNotfoundMessage = 'Job not found.'

export async function JobDetailPage({ params }: JobDetailPageProps) {
    const { jobId } = params;
    const job: Job | null = await getJobById(jobId);

    if (!job) {
        return <div className="text-center text-red-500 text-lg">{jobNotfoundMessage}</div>;
    }

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">{job.title}</h1>
            <p className="text-xl text-gray-700 mb-2">Company: {job.company}</p>
            <p className="text-gray-600 mb-4">Published: {new Date(job.created_at).toLocaleDateString()}</p>
            <p className="text-lg leading-relaxed">{job.description}</p>
            <a href={job.url} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline mt-4 block">
                Apply Here
            </a>
        </div>
    );
} 