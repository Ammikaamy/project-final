import { Routes, Route } from "react-router-dom";
import "./App.css";
import { getFirestore } from "firebase/firestore";
import LoginPage from "./components/LoginComponent";
import HomePage from "./components/HomePage";
import EditProfilePage from "./components/EditProfilePage";
import AddCourse from "./components/AddCourse";
import ManageClassroom from "./components/ManageClassroom";
import Question from "./components/Question";
import CheckIn from "./components/CheckIn";

function App() {

	return (
		<div>
			<Routes>
				<Route path="/" element={<LoginPage />} />
				<Route path="/home" element={<HomePage />} />
				<Route path="/edit-profile" element={<EditProfilePage/>} />
				<Route path="/add-course" element={<AddCourse/>} />
				<Route path="/manage-classroom/:id" element={<ManageClassroom />} /> 
				<Route path="/checkin/:classroomId/:checkinId" element={<CheckIn />} />
				<Route path="/checkin/:classroomId/:checkinId/question" element={<Question />} />
	
			</Routes>
		</div>
	);
}

export default App;
