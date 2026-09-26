import Sidebar from "../components/layout/Sidebar";
import MainContent from "../components/layout/MainContent";

function Home() {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <MainContent />
    </div>
  );
}

export default Home;