export enum AppStatus {
	Running = 'running',
	Stopped = 'stopped'
}

export type AppState = {
	status: AppStatus;
	name: string;
	cpuUsage: number;
	memoryUsage: number;
	containerCount: number;
	portsCount: number;
	volumesCount: number;
};
