import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Home from '@/app/page';
import * as jobService from '@/services/jobService';
import { Job } from '@/services/jobService.types';

jest.mock('@/services/jobService');

describe('Home page', () => {
    // Добавляем очистку моков перед каждым тестом для изоляции
    beforeEach(() => {
        jest.clearAllMocks();
    });

    const mockJobs: Job[] = [
        {
            id: 1,
            title: 'Senior Python Developer',
            company: 'FutureTech',
            url: 'http://example.com/1',
            created_at: new Date().toISOString(),
            description: 'A great job for a Python expert.',
        },
        {
            id: 2,
            title: 'React Ninja',
            company: 'CreativeMinds',
            url: 'http://example.com/2',
            created_at: new Date().toISOString(),
            description: 'A great job for a React expert.',
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

    // Наш новый "красный" тест
    it('should display a message when no jobs are found', async () => {
        (jobService.getJobs as jest.Mock).mockResolvedValue([]);

        const PageComponent = await Home();
        render(PageComponent);

        expect(screen.getByText('No jobs available at the moment.')).toBeInTheDocument();
        expect(jobService.getJobs).toHaveBeenCalledTimes(1);
    });
});