#include "dialog.h"
#include "ui_dialog.h"

#define R 5

///////////// Global Variables //////////////////

unsigned long globalTime = 0;               // Counting the loops
bool CONFIRM = false;

int numberOfNormalCars = 0 ;                // Self-explanatory

/* WARNING !!! Have to put at least ONE drunk vehicle */
int numberOfDrunkCars = 210;

int totalCars = numberOfDrunkCars + numberOfNormalCars;

///////////////////////////////////////////////

Dialog::Dialog(QWidget *parent) :
    QDialog(parent), ui(new Ui::Dialog)
{
    /////////////// System Settings ////////////////
    ui->setupUi(this);
    scene = new QGraphicsScene(this);
    ui->graphicsView->setScene(scene);
    scene->setSceneRect( -250, -250, 250*2, 250*2 );
    timer = new QTimer(this);
    connect(timer,SIGNAL(timeout()), this, SLOT(theLoop()));
    timer->start(1); // run in 1ms
    ///////////////// Initiations ////////////////
    /* Random settings */
    srand(time(NULL));

    /* Create a MAP object */
    p = new Path();

    /* Add number of NORMAL DRIVER into simulation */
    for(int i = 0; i < numberOfNormalCars; i++)
    {
        vehicles.push_back( new NormalDriver( rand() % 800 - 400, rand() % 800 - 400, 1, rand() % 3 + 1, p, globalTime));
    }
}


Dialog::~Dialog()
{
    delete ui;
}


void Dialog::theLoop(){

    ///////////// Graphics Settings ////////////////
    scene->clear();
    QPen darkCyan = QPen(Qt::darkCyan, 3);
    QPen yellow = QPen(Qt::yellow, 3);
    QPen lightGray = QPen(Qt::lightGray, 40);
    QPen darkMagenta = QPen(Qt::darkMagenta, 3);
    QPen black = QPen(Qt::black, 3);
    QPen red = QPen(Qt::red, 3);
    QPen blue = QPen(Qt::blue, 3);

    QString counterString;
    QString Pat;
    QString Cars;
    QString Acci;
    /////////////// Main Code here /////////////////

    /* Behavior of cars */
    run(vehicles, p);

    /* Argu 1: # of Drunk cars, Argu 2: at which Iteration */
    addExperiDriver(numberOfDrunkCars, 0);

    /* Stop simulation at X iteration */
    stopSimulation(2500);


    ////////////////// Collect Data //////////////////


    // writeDataVel(vehicles, "velocity1.csv","velocity", 1);
    // writeDataVel(vehicles, "patience1.csv","Patience", 1);

    // writeDataVel(vehicles, "velocity2.csv","velocity", 2);
    // writeDataVel(vehicles, "patience2.csv","Patience", 2);

    // writeDataVel(vehicles, "velocity0.csv","velocity", 0);
    // writeDataVel(vehicles, "patience0.csv","Patience", 0);

    // writeData(vehicles, "velocity.csv","velocity");
    // writeData(vehicles, "patience.csv","Patience");
    // writeData(vehicles, "Accidents.csv","AccidentsSeen");

    // writeDataVel(vehicles, "timeT.csv","TimeTaken");

    /// writeData Function writes data into a csv or a txt file ///
    // arguments (vehicle vector, "name.txt or name.csv", "variable to be recorded")
    // recordable variables- "velocity", "AccidentsSeen", "AccidentInvolved", "Patience", "TimeTaken

    if (globalTime == 2300)
    {
        writeData(vehicles, "time.csv","TimeTaken");
    }

    ////////////////  Draw Streets ////////////////
    /* Draw Streets */
    drawMap(lightGray, black);


    /* Showing the accessible points on the map, red means no way, yellow means o.k. (It's deactivated now) */
    // showJunctions( p, yellow, red);


    ////////////////  Draw Objects ////////////////

    /* Draw Destination : yellow/black */
    drawDest(p, yellow);

    /* Color the car by their speed / behavior */
    drawCars(vehicles, darkCyan, black, red, blue, yellow);

    //////////////////  Counter //////////////////

    /* Display info during simulation */
    counterString.setNum(globalTime);
    ui->label->setText("Global Time : " + counterString);
    globalTime++;

    Pat.setNum(vehicles[totalCars]->patience);
    ui->label_3->setText("Patience: " + Pat);
    Cars.setNum(vehicles[totalCars]->carsAroundMe);
    ui->label_4->setText("PossibleCars: " + Cars);
    Acci.setNum(vehicles[totalCars]->NumAccidentMet);
    ui->label_5->setText("NumAcciMet: " + Acci);
}


void Dialog::run(std::vector<Vehicle *> &vehicles, Path* p)
{
    for(std::vector<Vehicle*>::iterator i = vehicles.begin(); i < vehicles.end(); i++)
    {
        (*i)->chooseJunction(p);
        (*i)->makeTurn(p);
        (*i)->move(vehicles);
        (*i)->update();

        /* Move the cars outside of the map if it has reached the destination */
        if((*i)->reachedDest == true)
        {
            // vehicles.erase(i);
            (*i)->location->x = 450;
            (*i)->location->y = 450;
        }

        /* ove the cars outside of the map if one has been crashed for 300 loops */
        if((*i)->crashed == true && (globalTime - (*i)->memory) > 300) //
        {
            // vehicles.erase(i);
            // vehicles.push_back( new NormalDriver( rand() % 800 - 400, rand() % 800 - 400, 3, rand() % 4 + 1, p, globalTime) );
            (*i)->location->x = 450;
            (*i)->location->y = 450;
        }
    }
}

void Dialog::addExperiDriver(unsigned long numberOfExperiCars, unsigned long iteration)
{
    if(globalTime == iteration)
    {
        unsigned long a = numberOfExperiCars / 3;

        for(unsigned long i = 0; i < a; i++)
        {
            vehicles.push_back( new DrunkDriver( rand() % 800 - 400, rand() % 800 - 400, 0, rand() % 3 + 2, p, globalTime));
        }
        for(unsigned long i = 0; i < a; i++)
        {
            vehicles.push_back( new DrunkDriver( rand() % 800 - 400, rand() % 800 - 400, 1, rand() % 3 + 2, p, globalTime));
        }
        for(unsigned long i = 0; i < a; i++)
        {
            vehicles.push_back( new DrunkDriver( rand() % 800 - 400, rand() % 800 - 400, 2, rand() % 3 + 2, p, globalTime));
        }
        /* Vehicle with different color for demonstration */
        vehicles.push_back( new DrunkDriver( rand() % 800 - 400, rand() % 800 - 400, 3, rand() % 3 + 2, p, globalTime ));

        CONFIRM = true;
    }

    if(vehicles.size() == numberOfNormalCars && CONFIRM == true)
    {
        timer->stop();
    }
}

void Dialog::on_pushButton_clicked()
{
    if(timer->isActive())
    {
        timer->stop();
    }
    else
    {
        timer->start(1);
    }
}

void Dialog::drawMap(QPen lightGray, QPen black)
{
    scene->addLine(-400,-400,-400, 400, lightGray);
    scene->addLine(-400, 400, 400, 400, lightGray);
    scene->addLine( 400, 400, 400,-400, lightGray);
    scene->addLine( 400,-400,-400,-400, lightGray);
    scene->addLine(-400,   0, 400,   0, lightGray);
    scene->addLine(   0,-400,   0, 400, lightGray);
    scene->addLine(-200, 400,-200,-400, lightGray);
    scene->addLine( 200,-400, 200, 400, lightGray);
    scene->addLine(-400,-200, 400,-200, lightGray);
    scene->addLine(-400, 200, 400, 200, lightGray);

    scene->addLine(-400,-400,-400, 400, black);
    scene->addLine(-400, 400, 400, 400, black);
    scene->addLine( 400, 400, 400,-400, black);
    scene->addLine( 400,-400,-400,-400, black);
    scene->addLine(-400,   0, 400,   0, black);
    scene->addLine(   0,-400,   0, 400, black);
    scene->addLine(-400,-200, 400,-200, black);
    scene->addLine(-400, 200, 400, 200, black);
    scene->addLine( 200,-400, 200, 400, black);
    scene->addLine(-200, 400,-200,-400, black);
}

void Dialog::drawCars(std::vector<Vehicle *> &vehicles, QPen darkCyan, QPen black, QPen red, QPen blue, QPen yellow)
{
    std::vector<Vehicle*>::iterator i;

    for( i = vehicles.begin(); i < vehicles.end(); i++){

        if((*i)->crashed == true){
            scene->addEllipse((*i)->location->x -(R/2), (*i)->location->y - (R/2), R, R, red, QBrush(Qt::red));
        }
        else if((*i)->id == 1){
            scene->addEllipse((*i)->location->x -(R/2), (*i)->location->y - (R/2), R, R, blue, QBrush(Qt::blue));
        }
        else if((*i)->id == 2){
            scene->addEllipse((*i)->location->x -(R/2), (*i)->location->y - (R/2), R, R, darkCyan, QBrush(Qt::yellow));
        }
        else if((*i)->id == 3){
            scene->addEllipse((*i)->location->x -(R/2), (*i)->location->y - (R/2), R, R, black, QBrush(Qt::yellow));
        }
        else if((*i)->id == 0){
            scene->addEllipse((*i)->location->x -(R/2), (*i)->location->y - (R/2), R, R, yellow, QBrush(Qt::black));
        }
    }
}

void Dialog::drawDest(Path* p, QPen yellow)
{
    unsigned long numOfDest = p->Destinations.size();

    for(unsigned long i = 0; i < numOfDest; i++){
        scene->addEllipse(p->Destinations[i]->x -R, p->Destinations[i]->y - R, 2*R, 2*R, yellow, QBrush(Qt::black));
    }
}

void Dialog::showJunctions(Path* p, QPen yellow, QPen red)
{
    for(std::vector<Junction*>::iterator i = p->mainJunctions.begin(); i < p->mainJunctions.end(); i++){

        for(std::vector<JunctionPoint*>::iterator j = (*i)->subJunctions.begin(); j < (*i)->subJunctions.end(); j++){

            /* Alternatively, showing the in/out points at the junction, by changing the keyword from "accessible" to "inOrOut" */
            /* false = 0 stands for OUT, true = 1 stands for IN. */
            if((*j)->inOrOut == false) // <-- change it here
            {
                scene->addEllipse( (*j)->x -R, (*j)->y -R, 10, 10, red, QBrush(Qt::red));
            }
            else
            {
                scene->addEllipse( (*j)->x -R, (*j)->y -R, 10, 10, yellow, QBrush(Qt::yellow));
            }
        }
    }
}

void Dialog::on_verticalSlider_valueChanged(int value)
{
    timer->start(value);
}

void Dialog::stopSimulation(unsigned long time)
{
    if(globalTime == time)
    {
        timer->stop();
    }
}


void Dialog::writeDataVel(std::vector<Vehicle *> &vehicles, QString name, QString variable, int id)
{
    QString textData,dataS;

    if(variable == "velocity")
    {
        for (unsigned long j = 0; j < vehicles.size(); j++)
        {
            if(vehicles[j]->id == id)
            {
                if(j == vehicles.size()-1)
                {
                    textData +=  dataS.setNum(vehicles[j]->velocity->mag());
                }
                else
                {
                    textData +=  dataS.setNum(vehicles[j]->velocity->mag());
                    textData += ",  "  ;
                }
            }
        }
        textData += "\n";

        QFile file("/Users/arindam/QtProjects/AnotherApproach/"+name);
        if(file.open(QIODevice::Append))
        {
            QTextStream stream(&file);
            stream << textData;

        }
    }
    else if (variable == "TimeTaken")
    {
        for (unsigned long j = 0; j < vehicles.size(); j++)
        {
            if(vehicles[j]->id == id)
            {
                if(j==vehicles.size()-1)
                {
                    textData +=  dataS.setNum(vehicles[j]->localTime);
                }
                else
                {
                    textData +=  dataS.setNum(vehicles[j]->localTime);
                    textData += ",  "  ;
                }
            }
        }
        textData += "\n";

        QFile file("/Users/arindam/QtProjects/AnotherApproach/"+name);
        if(file.open(QIODevice::Append))
        {
            QTextStream stream(&file);
            stream << textData;
        }
    }
    else if (variable == "AccidentsSeen")
    {
        for (unsigned long j = 0; j < vehicles.size(); j++)
        {
            if(vehicles[j]->id == id)
            {
                if(j==vehicles.size()-1)
                {
                    textData +=  dataS.setNum(vehicles[j]->NumAccidentMet);
                }
                else
                {
                    textData +=  dataS.setNum(vehicles[j]->NumAccidentMet);
                    textData += ",  "  ;
                }
            }

        }
        textData += "\n";

        QFile file("/Users/arindam/QtProjects/AnotherApproach/"+name);
        if(file.open(QIODevice::Append))
        {
            QTextStream stream(&file);
            stream << textData;
        }
    }
    else if (variable == "Patience")
    {
        for (unsigned long j = 0; j < vehicles.size(); j++)
        {
            if(vehicles[j]->id == id)
            {
                if(j==vehicles.size()-1)
                {
                    textData +=  dataS.setNum(vehicles[j]->patience);
                }
                else
                {
                    textData +=  dataS.setNum(vehicles[j]->patience);
                    textData += ",  "  ;
                }
            }

        }
        textData += "\n";

        QFile file("/Users/arindam/QtProjects/AnotherApproach/"+name);
        if(file.open(QIODevice::Append))
        {
            QTextStream stream(&file);
            stream << textData;
        }
    }
}


void Dialog::writeData(std::vector<Vehicle *> &vehicles, QString name, QString variable)
{
    QString textData,dataS;

    if(variable == "velocity")
    {
        for (unsigned long j = 0; j < vehicles.size(); j++)
        {
            if(j == vehicles.size()-1)
            {
                textData +=  dataS.setNum(vehicles[j]->velocity->mag());
            }
            else
            {
                textData +=  dataS.setNum(vehicles[j]->velocity->mag());
                textData += ",  "  ;
            }
        }
        textData += "\n";

        QFile file("/Users/arindam/QtProjects/AnotherApproach/"+name);
        if(file.open(QIODevice::Append))
        {
            QTextStream stream(&file);
            stream << textData;
        }
    }
    else if (variable == "TimeTaken")
    {
        for (unsigned long j = 0; j < vehicles.size(); j++)
        {

            if(j==vehicles.size()-1)
            {
                textData +=  dataS.setNum(vehicles[j]->lot);
            }
            else
            {
                textData +=  dataS.setNum(vehicles[j]->lot);
                textData += ",  "  ;
            }
        }
        textData += "\n";

        QFile file("/Users/arindam/QtProjects/AnotherApproach/"+name);
        if(file.open(QIODevice::Append))
        {
            QTextStream stream(&file);
            stream << textData;
        }
    }
    else if (variable == "AccidentsSeen")
    {
        for (unsigned long j = 0; j < vehicles.size(); j++)
        {

            if(j==vehicles.size()-1)
            {
                textData +=  dataS.setNum(vehicles[j]->numOfAcc);
            }
            else
            {
                textData +=  dataS.setNum(vehicles[j]->numOfAcc);
                textData += ",  "  ;
            }

        }
        textData += "\n";

        QFile file("/Users/arindam/QtProjects/AnotherApproach/"+name);
        if(file.open(QIODevice::Append))
        {
            QTextStream stream(&file);
            stream << textData;
        }
    }
    else if (variable == "Patience")
    {
        for (unsigned long j = 0; j < vehicles.size(); j++)
        {
            if(j==vehicles.size()-1)
            {
                textData +=  dataS.setNum(vehicles[j]->patience);
            }
            else
            {
                textData +=  dataS.setNum(vehicles[j]->patience);
                textData += ",  "  ;
            }

        }
        textData += "\n";

        QFile file("/Users/arindam/QtProjects/AnotherApproach/"+name);
        if(file.open(QIODevice::Append))
        {
            QTextStream stream(&file);
            stream << textData;
        }
    }
}
