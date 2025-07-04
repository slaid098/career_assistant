import { getJobs } from "@/services/jobService";

export default async function Home() {
  const jobs = await getJobs();

  return (
    <main>
      <h1>Job Listings</h1>
      {jobs.map((job) => (
        <div key={job.id}>
          <h2>{job.title}</h2>
          <p>{job.company}</p>
        </div>
      ))}
    </main>
  );
}
