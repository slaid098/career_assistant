import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { JobDetailPage, jobNotfoundMessage } from '@/app/jobs/[jobId]/page';
import * as jobService from '@/services/jobService';
import { Job } from '@/services/jobService.types';

jest.mock('@/services/jobService');

describe('Job Detail Page', () => {

    beforeEach(() => {
        jest.clearAllMocks();
    });

    const mockJob: Job = {
        id: 1,
        title: 'Senior Python Developer',
        company: 'FutureTech',
        url: 'http://example.com/1',
        created_at: new Date().toISOString(),
        description: 'A great job for a Python expert.',
    };

    it('should fetch a single job on the server and display its details', async () => {
        (jobService.getJobById as jest.Mock).mockResolvedValue(mockJob);

        const PageComponent = await JobDetailPage({ params: { jobId: '1' } });
        render(PageComponent);

        expect(screen.getByText('Senior Python Developer')).toBeInTheDocument();
        expect(screen.getByText(/FutureTech/i)).toBeInTheDocument();
        expect(screen.getByText('A great job for a Python expert.')).toBeInTheDocument();

        expect(jobService.getJobById).toHaveBeenCalledWith('1');
        expect(jobService.getJobById).toHaveBeenCalledTimes(1);
    });

    it('should display "Job not found" when the job does not exist', async () => {
        (jobService.getJobById as jest.Mock).mockResolvedValue(null);
        const PageComponent = await JobDetailPage({ params: { jobId: '1' } });
        render(PageComponent);

        expect(screen.getByText(jobNotfoundMessage)).toBeInTheDocument();
        expect(jobService.getJobById).toHaveBeenCalledWith('1');
        expect(jobService.getJobById).toHaveBeenCalledTimes(1);
    });
}); 