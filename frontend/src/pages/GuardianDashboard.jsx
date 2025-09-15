import { useState, useEffect } from 'react';
import { getStudents, getTrips } from '../api/api';
import StudentGrid from '../components/StudentGrid';
import MapView from '../components/MapView';

const GuardianDashboard = () => {
  const [students, setStudents] = useState([]);
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [studentsData, tripsData] = await Promise.all([
          getStudents(),
          getTrips()
        ]);
        setStudents(studentsData);
        setTrips(tripsData);
      } catch (err) {
        setError('Failed to fetch data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Guardian Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h2 className="text-xl font-semibold mb-4">Your Students</h2>
          <StudentGrid students={students} />
        </div>
        
        <div>
          <h2 className="text-xl font-semibold mb-4">Active Trips</h2>
          {trips.map(trip => (
            <div key={trip.id} className="mb-6">
              <h3 className="text-lg font-medium mb-2">Trip #{trip.id}</h3>
              <MapView location={trip.currentLocation} />
              <div className="mt-2 text-sm text-gray-600">
                <p>Status: {trip.status}</p>
                <p>ETA: {new Date(trip.estimatedArrival).toLocaleTimeString()}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default GuardianDashboard;
