import React from 'react';
import Link from 'next/link';
import { Job } from '@/services/jobService.types';

type JobCardProps = {
  job: Job;
};

const JobCard: React.FC<JobCardProps> = ({ job }) => {
  return (
    <Link href={`/jobs/${job.id}`} className="block p-4 border rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200">
      <h2 className="text-xl font-semibold">{job.title}</h2>
      <p className="text-gray-600">{job.company}</p>
    </Link>
  );
};

export default JobCard; 