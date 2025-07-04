import { getJobs } from "@/services/jobService";
import JobCard from "@/components/JobCard";

export default async function Home() {
  const jobs = await getJobs();

  return (
    <main>
      <h1>Job Listings</h1>
      {jobs.map((job) => (
        <JobCard key={job.id} job={job} />
      ))}
    </main>
  );
}
