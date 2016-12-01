#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <math.h>

struct City {
	int num;
	int xCoord;
	int yCoord;
	bool visited;
	int distToNext;
	City *prev;
	City *next;
};
struct Path {
	City *origin;
	int numCities;
	int distance;
};

City *createCity(int num, int xCoord, int yCoord);
Path *createPath();
void readFile(std::string inFileName, std::vector<City*> &cities);
void resetVisited(std::vector<City*> &cities);
void resetVisited(Path *path);
int findPathDistance(Path *path);
int findDistance(City *city1, City *city2);
void greedyPath(std::vector<City*> &cities, Path *path);
void opt2Path(Path *path);
void doSwap(City *city1, City *city2);

City *createCity(int num, int xCoord, int yCoord){
	City *newCity = new City;
	newCity->num = num;
	newCity->xCoord = xCoord;
	newCity->yCoord = yCoord;
	newCity->visited = false;
	newCity->distToNext = 0;
	newCity->prev = NULL;
	newCity->next = NULL;
	return newCity;
}

Path *createPath(){
	Path *path = new Path;
	path->origin = NULL;
	path->numCities = 0;
	path->distance = 0;
	return path;
}

void resetVisited(std::vector<City*> &cities){
	for(int i=0; i<cities.size(); i++){
		cities[i]->visited = false;
	}
}
void resetVisited(Path *path){
	City *current = path->origin;
	while(current->visited){
		current->visited = false;
		current = current->next;
	}
}
int findPathDistance(Path *path){
	City *current = path->origin->next;
	int dist = path->origin->distToNext;
	while(path->origin != current){
		dist += current->distToNext;
		current = current->next;
	}
	return dist;
}
int findDistance(City *city1, City *city2){
	return sqrt(pow((city2->xCoord - city1->xCoord),2) + pow((city2->yCoord - city1->yCoord),2));
}

void readFile(std::string inFileName, std::vector<City*> &cities){
	std::ifstream inFile;
	std::string line;
	std::vector<std::string> fileLines;
	
	inFile.open(inFileName);
	if(inFile.is_open()){
		while(std::getline(inFile, line)){
			if(line != "" && line != "\r" && line != "\n")
				fileLines.push_back(line);
		}
		inFile.close();
		
		int cityData[3];
		int num, xCoord, yCoord;
		for(int i=0; i<fileLines.size(); i++){
			int slot = 0;
			std::string temp = "";
			int j=0;
			std::stringstream ss(fileLines[i]);
			while(ss >> num){
				cityData[slot] = num;
				slot++;
			}
			cities.push_back(createCity(cityData[0], cityData[1], cityData[2]));
		}
	}
}

void greedyPath(std::vector<City*> &cities, Path *path){
	resetVisited(path);
	path->origin = cities[0];
	path->origin->visited = true;
	City *current = path->origin;
	int minDist = 9999999;
	int minSlot = 0;
	int totalVisited = 1;
	int currDist;
	while(totalVisited < cities.size()){
		for(int i=1; i<cities.size(); i++){
			if(!cities[i]->visited){
				currDist = findDistance(current, cities[i]);
				if(currDist < minDist && currDist != 0){
					path->origin->prev = cities[i];
					current->next = cities[i];
					current->distToNext = currDist;
					citites[i]->prev = current;
					citites[i]->next = path->origin;
					//minDist = currDist;
					//minSlot = i;
				}
			}
		}
		//current->next = cities[minSlot];
		//current->distToNext = minDist;
		//cities[minSlot]->prev = current;
		current = current->next;
		current->visited = true;
		totalVisited++;
	}
	//path->origin->prev = current;
	//current->next = path->origin;
	path->numCities = totalVisited;
	path->distance = findPathDistance(path);
}

void doSwap(City *city1, City *city2){
	City *temp;
	city1->prev->next = city2;
	city2->prev->next = city1;
	temp = city2->prev;
	city2->prev = city1->prev;
	city1->prev = temp;
	city1->next->prev = city2;
	city2->next->prev = city1;
	temp = city2->next;
	city2->next = city1->next;
	city1->next = temp;
}
void opt2Path(Path *path){
	int currDist = path->distance;
	Path *newPath = createPath();
	newPath = path;
	City *temp;
	City *current = newPath->origin->next;
	City *swapper = current->next;
	while(current != path->origin){
		while(!swapper->visited){
			doSwap(current, swapper);
			int newDist = findPathDistance(newPath);
			if(newDist < currDist){
				path = newPath;
			}
			else{
				doSwap(current, swapper);
			}
			swapper = swapper->next;
		}
		resetVisited(newPath);
		current = current->next;
	}
}

void print(Path *path){
	resetVisited(path);
	std::cout << path->distance << std::endl;
	City *current = path->origin;
	while(!current->visited){
		std::cout << current->num << " " << current->xCoord << " " << current->yCoord << std::endl;
		current->visited = true;
	}
}
void print(std::vector<City*> cities){
	for(int i=0; i<cities.size(); i++){
		std::cout << cities[i]->num << " " << cities[i]->xCoord << " " << cities[i]->yCoord << std::endl;
	}
}

int main(int argc, char *argv[]){
	std::string inFileName;
	std::string outFileName;
	std::ofstream outFile;
	std::vector<City*> cities;
	Path *path = createPath();
	
	if (argc < 2){
		std::cerr << "Please include the input file name.\n";
		return 1;
	}
	inFileName = argv[1];
	outFileName = inFileName + ".tour";
	readFile(inFileName, cities);
	
	greedyPath(cities, path);
	print(path);
	resetVisited(path);;
	//opt2Path(path);
	//print(path);
	
	resetVisited(path);
	outFile.open(outFileName);
	outFile << path->distance << std::endl;
	City *current = path->origin;
	while(!current->visited){
		outFile << current->num << std::endl;
		current->visited = true;
	}
	outFile.close();
}