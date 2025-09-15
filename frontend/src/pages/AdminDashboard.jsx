import { useState, useEffect } from 'react';
import { getAllGuardians, getAllStudents, getAllBuses } from '../api/api';
import { DataGrid } from '@mui/x-data-grid';

const AdminDashboard = () => {
  const [guardians, setGuardians] = useState([]);
  const [students, setStudents] = useState([]);
  const [buses, setBuses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [guardiansData, studentsData, busesData] = await Promise.all([
          getAllGuardians(),
          getAllStudents(),
          getAllBuses()
        ]);
        setGuardians(guardiansData);
        setStudents(studentsData);
        setBuses(busesData);
      } catch (err) {
        setError('Failed to fetch data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const guardianColumns = [
    { field: 'id', headerName: 'ID', width: 90 },
    { field: 'name', headerName: 'Name', width: 130 },
    { field: 'email', headerName: 'Email', width: 200 },
    { field: 'phoneNumber', headerName: 'Phone', width: 130 },
    { field: 'address', headerName: 'Address', width: 200 }
  ];

  const studentColumns = [
    { field: 'id', headerName: 'ID', width: 90 },
    { field: 'name', headerName: 'Name', width: 130 },
    { field: 'guardianName', headerName: 'Guardian', width: 130 },
    { field: 'grade', headerName: 'Grade', width: 90 },
    { field: 'busNumber', headerName: 'Bus #', width: 90 }
  ];

  const busColumns = [
    { field: 'id', headerName: 'ID', width: 90 },
    { field: 'number', headerName: 'Bus Number', width: 130 },
    { field: 'capacity', headerName: 'Capacity', width: 110 },
    { field: 'driverName', headerName: 'Driver', width: 130 },
    { field: 'status', headerName: 'Status', width: 110 }
  ];

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Admin Dashboard</h1>
      
      <div className="space-y-8">
        <div>
          <h2 className="text-xl font-semibold mb-4">Guardians</h2>
          <div style={{ height: 400 }}>
            <DataGrid
              rows={guardians}
              columns={guardianColumns}
              pageSize={5}
              rowsPerPageOptions={[5]}
              checkboxSelection
              disableSelectionOnClick
            />
          </div>
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-4">Students</h2>
          <div style={{ height: 400 }}>
            <DataGrid
              rows={students}
              columns={studentColumns}
              pageSize={5}
              rowsPerPageOptions={[5]}
              checkboxSelection
              disableSelectionOnClick
            />
          </div>
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-4">Buses</h2>
          <div style={{ height: 400 }}>
            <DataGrid
              rows={buses}
              columns={busColumns}
              pageSize={5}
              rowsPerPageOptions={[5]}
              checkboxSelection
              disableSelectionOnClick
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
