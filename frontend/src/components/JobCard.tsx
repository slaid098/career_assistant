import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Job } from '@/services/jobService.types';

type JobCardProps = {
  job: Job;
};

const JobCard: React.FC<JobCardProps> = ({ job }) => {
  const postDate = new Date(job.created_at);
  const formattedDate = postDate.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return (
    <Link 
      href={`/jobs/${job.id}`} 
      className="block bg-white p-6 border border-gray-200 rounded-lg shadow-sm hover:shadow-lg transition-all duration-300 ease-in-out transform hover:-translate-y-1"
    >
      <div className="flex items-start">
        <div className="flex-shrink-0 mr-4">
          <Image src="/globe.svg" alt={`${job.company} logo`} width={56} height={56} className="rounded-full" />
        </div>
        <div className="flex-grow">
          <h2 className="text-xl font-bold text-gray-800">{job.title}</h2>
          <p className="text-md text-gray-600 mt-1">{job.company}</p>
          <p className="text-sm text-gray-500 mt-2">Posted on {formattedDate}</p>
        </div>
      </div>
    </Link>
  );
};

export default JobCard; 