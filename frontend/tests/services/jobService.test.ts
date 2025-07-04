import { getJobs } from '@/services/jobService';
import { Job } from '@/services/jobService.types';
import fetchMock from 'jest-fetch-mock';

// Описываем группу тестов для 'jobService'
describe('jobService', () => {
  // Перед каждым тестом в этой группе очищаем все моки
  beforeEach(() => {
    fetchMock.resetMocks();
  });

  // Описываем конкретный тест: 'должен получать и возвращать список вакансий'
  it('should fetch and return a list of jobs', async () => {
    // 1. Arrange (Подготовка)
    const mockJobs: Job[] = [
      {
        id: 1,
        title: 'Python Developer',
        url: 'http://example.com/job/1',
        company: 'Example Corp',
        created_at: new Date().toISOString(),
      },
      {
        id: 2,
        title: 'Frontend Developer',
        url: 'http://example.com/job/2',
        company: 'Another Corp',
        created_at: new Date().toISOString(),
      },
    ];

    // Говорим нашему моку fetch, чтобы при следующем вызове он вернул 'mockJobs' в формате JSON
    fetchMock.mockResponseOnce(JSON.stringify(mockJobs));

    // 2. Act (Действие)
    // Вызываем функцию, которую мы тестируем (она еще не существует, поэтому будет ошибка)
    const jobs = await getJobs();

    // 3. Assert (Проверка)
    // Проверяем, что fetch был вызван с правильным URL
    expect(fetchMock.mock.calls.length).toBe(1);
    const expectedUrl = new URL('/jobs', process.env.NEXT_PUBLIC_API_BASE_URL!).toString();
    expect(fetchMock.mock.calls[0][0]).toBe(expectedUrl);

    // Проверяем, что наша функция вернула именно те данные, которые мы "подсунули" в мок
    expect(jobs).toEqual(mockJobs);
  });
});