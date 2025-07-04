import React from 'react';
import { Job } from '@/services/jobService.types';

type JobCardProps = {
  job: Job;
};

const JobCard: React.FC<JobCardProps> = ({ job }) => {
  return (
    <div>
      <h2>{job.title}</h2>
      <p>{job.company}</p>
    </div>
  );
};

export default JobCard; 