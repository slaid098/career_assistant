import { getJobs } from "@/services/jobService";
import JobCard from "@/components/JobCard";

export default async function Home() {
  const jobs = await getJobs();

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-8 text-center">Available Jobs</h1>
      {jobs.length === 0 ? (
        <p className="text-center text-gray-500">No jobs available at the moment.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {jobs.map((job) => (
            <JobCard key={job.id} job={job} />
          ))}
        </div>
      )}
    </main>
  );
}
