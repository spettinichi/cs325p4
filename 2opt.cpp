#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>

struct City {
	int num;
	int xCoord;
	int yCoord;
	bool visited;
	int distToNext;
	City *prev;
	City *next;
}
struct Path {
	City *origin;
	int numCities;
	int distance;
}

City creatCity(int num, int xCoord, int yCoord);
void readFile(std::string inFileName, std::vector<City> &cities);
void resetVisited(std::vector<City> &cities);
void resetVisited(Path &path);
int findPathDistance(Path &path);
int findDistance(City &city1, City &city2);
void greedyPath(std::vector<City> &cities, Path &path);
void opt2Path(std::vector<City> &cities, Path &path);
void doSwap(City *city1, City *city2);

City creatCity(int num, int xCoord, int yCoord){
	City newCity = new City;
	newCity.num = num;
	newCity.xCoord = xCoord;
	newCity.yCoord = yCoord;
	newCity.visited = false;
	newCity.distToNext = 0;
	newCity.prev = NULL;
	newCity.next = NULL;
	return newCity;
}

Path createPath(){
	Path path = new Path;
	path.origin = NULL;
	path.numCities = 0;
	path.distance = 0;
	return path;
}

void resetVisited(std::vector<City> &cities){
	for(int i=0; i<cities.size(); i++){
		cities[i].visited = false;
	}
}
void resetVisited(Path &path){
	path.origin.visited = false;
	City *current = path.origin.next;
	while(path.origin != current){
		current.visited = false;
	}
}
int findPathDistance(Path &path){
	City *current = path.origin.next;
	int dist = path.origin.distToNext;
	while(path.origin != current){
		dist += current.distToNext;
		current = current.next;
	}
	return dist;
}
int findDistance(City &city1, City &city2){
	return sqrt((city2.xCoord - city1.xCoord)^2 + (city2.yCoord - city1.yCoord)^2)
}

void readFile(std::string inFileName, std::vector<City> &cities){
	std::ifstream inFile;
	std::string line;
	std::vector<std::string> fileLines;
	
	infile.open(inFileName);
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
			for(int j=0; fileLines[i][j] != '\n'; j++){
				if (fileLines[i][j] != ' '){
					temp += fileLines[i][j];
				}
				else {
					std::stringstream ss(temp);
					ss >> cityData[slot];
					slot++;
				}
			}
			cities.push_back(createCity(cityData[0], cityData[1], cityData[2]));
		}
	}
}

void greedyPath(std::vector<City> &cities, Path &path){
	path.origin = cities[0];
	path.origin.visited = true;
	City *current;
	current = Path.origin;
	int minDist = 999999;
	int minSlot = 0;
	int totalVisited = 1;
	int currDist;
	while(totalVisited < cities.size()-1){
		for(int i=1; i<cities.size(); i++){
			if(!cities[i].visited){
				currDist = findDistance(current, cities[i]);
				if(currDist < minDist && currDist != 0){
					minDist = currDist;
					minSlot = i;
				}
			}
		}
		current.next = cities[minSlot];
		current.distToNext = minDist;
		cities[minSlot].prev = current;
		current = current.next;
		current.visited = true;
		totalVisited++;
	}
	path.origin.prev = current;
	current.next = path.origin;
	path.numCities = totalVisited;
	path.distance = findPathDistance(path);
}

void doSwap(City *city1, City *city2){
	City *temp;
	city1.prev.next = city2;
	city2.prev.next = city1;
	temp = city2.prev;
	city2.prev = city1.prev;
	city1.prev = temp;
	city1.next.prev = city2;
	city2.next.prev = city1;
	temp = city2.next;
	city2.next = city1.next;
	city1.next = temp;
}

void opt2Path(Path &path){
	int currDist = path.distance;
	Path newPath = createPath;
	newPath = path;
	City *temp;
	City *current = newPath.origin.next;
	City *swapper = current.next;
	while(current != path.origin){
		while(swapper != path.origin){
			doSwap(current, swapper);
			int newDist = findPathDistance(newPath);
			if(newDist < currDist){
				path = newPath;
			}
			else{
				doSwap(current, swapper);
			}
			swapper = swapper.next;
		}
		current = current.next;
	}
}

int main(int argc, char *argv[]){
	std::string inFileName;
	std::string outFileName;
	std::ofstream outFile;
	std::vector<City> cities;
	Path path = createPath;
	
	if (argc < 2){
		std::cerr << "Please include the input file name.\n";
		return 1;
	}
	inFileName = argv[1];
	outFileName = inFileName + ".tour";
	readFile(inFileName, cities);
	
	greedyPath(cities, path);
	resetVisited(path);
	opt2Path(path);
	
	outFile.open(outFileName);
	outFile << path.distance << endl;
	outFile << path.origin.num;
	City *current = path.origin.next;
	while(current != path.origin)
		outFile << current.num << endl;
	outFile.close();
}