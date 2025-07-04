import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import JobCard from '@/components/JobCard';
import { Job } from '@/services/jobService.types';

describe('JobCard component', () => {
  const mockJob: Job = {
    id: 1,
    title: 'Senior Software Engineer',
    company: 'Innovate Inc.',
    url: 'https://example.com/job/1',
    created_at: new Date().toISOString(),
  };

  it('should render the job title and company name', () => {
    render(<JobCard job={mockJob} />);

    expect(screen.getByText('Senior Software Engineer')).toBeInTheDocument();
    expect(screen.getByText('Innovate Inc.')).toBeInTheDocument();
  });
}); 