import { getJobById } from '@/services/jobService';
import { Job } from '@/services/jobService.types';
import Image from 'next/image';

interface JobDetailPageProps {
    params: {
        jobId: string;
    };
}
export const jobNotfoundMessage = 'Job not found.'

export default async function JobDetailPage({ params }: JobDetailPageProps) {
    const { jobId } = params;
    const job: Job | null = await getJobById(jobId);

    if (!job) {
        return <div className="text-center text-red-500 text-lg">{jobNotfoundMessage}</div>;
    }

    return (
        <div className="bg-white p-8 rounded-lg shadow-md max-w-4xl mx-auto">
            <div className="flex items-start mb-6">
                <div className="flex-shrink-0 mr-6">
                    <Image src="/globe.svg" alt={`${job.company} logo`} width={80} height={80} className="rounded-full" />
                </div>
                <div>
                    <h1 className="text-4xl font-extrabold text-gray-800">{job.title}</h1>
                    <p className="text-2xl text-gray-600 mt-1">{job.company}</p>
                </div>
            </div>

            <div className="border-t border-gray-200 pt-6">
                <div className="mb-6">
                    <h2 className="text-2xl font-semibold text-gray-700 mb-3">Job Description</h2>
                    <div className="prose prose-lg max-w-none text-gray-600 leading-relaxed" dangerouslySetInnerHTML={{ __html: job.description }} />
                </div>
                
                <div className="flex justify-between items-center mt-8">
                    <p className="text-md text-gray-500">
                        Posted on: {new Date(job.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
                    </p>
                    <a 
                        href={job.url} 
                        target="_blank" 
                        rel="noopener noreferrer" 
                        className="inline-block bg-blue-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors duration-300 shadow-lg"
                    >
                        Apply Now
                    </a>
                </div>
            </div>
        </div>
    );
} 