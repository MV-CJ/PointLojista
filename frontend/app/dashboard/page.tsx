'use client';

import { useUserProfile } from '../services/auth';

const DashboardPage = () => {
  const { userProfile, profileError, isLoading } = useUserProfile();

  if (isLoading) {
    return <p>Carregando...</p>;
  }

  if (profileError) {
    return <p className="text-red-500">{profileError}</p>;
  }

  return (
    <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
      {/* Restante do conteúdo do dashboard */}
      <div className="grid auto-rows-min gap-4 md:grid-cols-3">
        <div className="aspect-video rounded-xl bg-muted/50" />
        <div className="aspect-video rounded-xl bg-muted/50" />
        <div className="aspect-video rounded-xl bg-muted/50" />
      </div>
      <div className="min-h-[100vh] flex-1 rounded-xl bg-muted/50 md:min-h-min" />
    </div>
  );
};

export default DashboardPage;