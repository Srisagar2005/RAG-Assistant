import Home from "./pages/Home";
import { DocumentsProvider } from "./context/DocumentsContext";

function App() {
  return (
    <DocumentsProvider>
      <Home />
    </DocumentsProvider>
  );
}

export default App;