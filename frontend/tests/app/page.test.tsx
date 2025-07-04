import { render } from '@testing-library/react';
import { screen } from '@testing-library/dom';
import '@testing-library/jest-dom';
import Home from '@/app/page';
import * as jobService from '@/services/jobService';
import { Job } from '@/services/jobService.types';

jest.mock('@/services/jobService');

describe('Home page', () => {

    const mockJobs: Job[] = [
        {
            id: 1,
            title: 'Senior Python Developer',
            company: 'FutureTech',
            url: 'http://example.com/1',
            created_at: new Date().toISOString(),
        },
        {
            id: 2,
            title: 'React Ninja',
            company: 'CreativeMinds',
            url: 'http://example.com/2',
            created_at: new Date().toISOString(),
        },
    ];

    it('should fetch jobs on the server and display them', async () => {
        (jobService.getJobs as jest.Mock).mockResolvedValue(mockJobs);

        const PageComponent = await Home();
        render(PageComponent);

        expect(screen.getByText('Senior Python Developer')).toBeInTheDocument();

        expect(screen.getByText('CreativeMinds')).toBeInTheDocument();

        expect(jobService.getJobs).toHaveBeenCalledTimes(1);
    });
});